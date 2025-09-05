<?php
$password = "Fpt1409!@";
$expected = "7fdaa4b045c8ff402b4459e51a2583072782eae0705b48c42998913bbf183301";

echo "Password: $password\n";
echo "Expected: $expected\n\n";

// Test different hash methods
$methods = [
    'md5' => md5($password),
    'sha1' => sha1($password),
    'sha256' => hash('sha256', $password),
    'sha256 with serein' => hash('sha256', $password . 'serein'),
    'hmac sha256' => hash_hmac('sha256', $password, 'serein'),
    'hmac sha256 with different key' => hash_hmac('sha256', $password, 'Fpt1409!@'),
    'double hash' => hash('sha256', hash('sha256', $password)),
    'hash with salt' => hash('sha256', $password . 'salt'),
];

foreach ($methods as $method => $hash) {
    if ($hash === $expected) {
        echo "✅ FOUND: $method = $hash\n";
    } else {
        echo "❌ $method = $hash\n";
    }
}
?>
