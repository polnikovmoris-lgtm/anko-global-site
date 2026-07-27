<?php
/*
 * Защищённый обработчик заявок.
 * Настройка получателя и, при необходимости, Telegram выполняется через
 * переменные окружения хостинга — см. inc/config.php и README.md.
 */
declare(strict_types=1);

require_once __DIR__ . '/inc/config.php';

header('Content-Type: application/json; charset=UTF-8');
header('Cache-Control: no-store, max-age=0');
header('X-Robots-Tag: noindex, nofollow', true);

function respond(int $status, array $payload): void {
    http_response_code($status);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

function clean_text($value, int $limit): string {
    $value = is_string($value) ? trim($value) : '';
    $value = preg_replace('/[\x00-\x1F\x7F]/u', ' ', $value) ?? '';
    return function_exists('mb_substr') ? mb_substr($value, 0, $limit) : substr($value, 0, $limit);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(405, ['error' => 'Метод не поддерживается.']);
}

$contentLength = (int) ($_SERVER['CONTENT_LENGTH'] ?? 0);
if ($contentLength > 65536) {
    respond(413, ['error' => 'Размер запроса превышает допустимый.']);
}

$contentType = $_SERVER['CONTENT_TYPE'] ?? '';
$data = strpos($contentType, 'application/json') !== false
    ? json_decode((string) file_get_contents('php://input'), true)
    : $_POST;

if (!is_array($data)) {
    respond(400, ['error' => 'Некорректные данные формы.']);
}

/* Honeypot: реальный посетитель это поле не видит. */
if (clean_text($data['company'] ?? '', 200) !== '') {
    respond(200, ['ok' => true]);
}

if (!hash_equals($_SESSION['csrf_token'] ?? '', clean_text($data['csrf'] ?? '', 128))) {
    respond(419, ['error' => 'Сессия формы устарела. Обновите страницу и попробуйте снова.']);
}

$name = clean_text($data['name'] ?? '', 100);
$phone = clean_text($data['phone'] ?? '', 50);
$message = clean_text($data['message'] ?? '', 2000);
$product = clean_text($data['product'] ?? '', 250);
$page = clean_text($data['page'] ?? '', 250);
$urlRaw = clean_text($data['url'] ?? '', 2048);
$url = filter_var($urlRaw, FILTER_VALIDATE_URL) ?: '';
$consentAccepted = in_array($data['consent'] ?? null, [1, '1', true, 'true', 'on'], true);

if (!$consentAccepted) {
    respond(422, ['error' => 'Подтвердите согласие на обработку персональных данных.']);
}

$policyVersion = '2026-07-26';
$consentTimeUtc = gmdate('c');

$digits = preg_replace('/\D+/', '', $phone);
if ((function_exists('mb_strlen') ? mb_strlen($phone) : strlen($phone)) < 7 || strlen($digits) < 7) {
    respond(422, ['error' => 'Укажите корректный номер телефона.']);
}

$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$rateFile = sys_get_temp_dir() . '/anko-lead-' . hash('sha256', $ip);
$now = time();
$rateHandle = @fopen($rateFile, 'c+');
if ($rateHandle === false || !flock($rateHandle, LOCK_EX)) {
    if (is_resource($rateHandle)) {
        fclose($rateHandle);
    }
    error_log('ANKO lead: rate-limit storage is unavailable.');
    respond(503, ['error' => 'Отправка временно недоступна. Позвоните нам по телефону на сайте.']);
}
$storedAttempts = stream_get_contents($rateHandle);
$attempts = json_decode($storedAttempts === false ? '' : $storedAttempts, true);
$attempts = is_array($attempts)
    ? array_values(array_filter($attempts, static fn($ts) => is_int($ts) && $ts > $now - 3600))
    : [];
if (count($attempts) >= 5) {
    flock($rateHandle, LOCK_UN);
    fclose($rateHandle);
    respond(429, ['error' => 'Слишком много заявок. Позвоните нам по телефону на сайте.']);
}

$attempts[] = $now;
$ratePayload = json_encode($attempts);
$rateSaved = $ratePayload !== false
    && ftruncate($rateHandle, 0)
    && rewind($rateHandle)
    && fwrite($rateHandle, $ratePayload) !== false
    && fflush($rateHandle);
flock($rateHandle, LOCK_UN);
fclose($rateHandle);
if (!$rateSaved) {
    error_log('ANKO lead: rate-limit state could not be saved.');
    respond(503, ['error' => 'Отправка временно недоступна. Позвоните нам по телефону на сайте.']);
}

$subject = 'Новая заявка с сайта ANKO GLOBAL';
$body = "Новая заявка с сайта\n\n"
    . "Имя: " . ($name ?: 'не указано') . "\n"
    . "Телефон: " . $phone . "\n"
    . "Товар / тема: " . ($product ?: 'не указано') . "\n"
    . ($message ? "Комментарий: " . $message . "\n" : '')
    . "Страница: " . ($page ?: 'не указано') . "\n"
    . "URL: " . ($url ?: 'не указано') . "\n"
    . "Согласие на обработку данных: подтверждено\n"
    . "Редакция политики: " . $policyVersion . "\n"
    . "Время согласия (UTC): " . $consentTimeUtc . "\n";

$to = filter_var($LEAD['to_email'], FILTER_VALIDATE_EMAIL);
$from = filter_var($LEAD['from_email'], FILTER_VALIDATE_EMAIL);
if (!$to || !$from) {
    error_log('ANKO lead: mail configuration is invalid.');
    respond(503, ['error' => 'Отправка временно недоступна. Позвоните нам по телефону на сайте.']);
}

$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'From: ANKO GLOBAL <' . $from . '>',
    'Reply-To: ' . $from,
];

if (!mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers))) {
    error_log('ANKO lead: mail() failed.');
    respond(503, ['error' => 'Не удалось отправить заявку. Позвоните нам по телефону на сайте.']);
}

/* Telegram — необязательная серверная копия. Токен в браузер не попадает. */
if ($LEAD['tg_token'] !== '' && $LEAD['tg_chat_id'] !== '') {
    $payload = json_encode(['chat_id' => $LEAD['tg_chat_id'], 'text' => $body], JSON_UNESCAPED_UNICODE);
    $context = stream_context_create(['http' => [
        'method'  => 'POST',
        'header'  => "Content-Type: application/json\r\n",
        'content' => $payload,
        'timeout' => 5,
    ]]);
    @file_get_contents('https://api.telegram.org/bot' . rawurlencode($LEAD['tg_token']) . '/sendMessage', false, $context);
}

respond(200, ['ok' => true]);
