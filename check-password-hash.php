<?php
// Check password hash for Fpt1409!@
$password = 'Fpt1409!@';

// Check different hash methods
echo "Password: $password\n";
echo "MD5: " . md5($password) . "\n";
echo "SHA1: " . sha1($password) . "\n";
echo "SHA256: " . hash('sha256', $password) . "\n";
echo "PASSWORD_DEFAULT: " . password_hash($password, PASSWORD_DEFAULT) . "\n";
echo "PASSWORD_BCRYPT: " . password_hash($password, PASSWORD_BCRYPT) . "\n";

// Check against existing hashes in database
$existing_hashes = [
    '7fdaa4b045c8ff402b4459e51a2583072782eae0705b48c42998913bbf183301',
    '52be5ff91284c65bac56f280df55f797a5c505f7ef66317ff358e34791507027'
];

echo "\nChecking against existing hashes:\n";
foreach ($existing_hashes as $hash) {
    echo "Hash: $hash\n";
    echo "  MD5 match: " . (md5($password) === $hash ? 'YES' : 'NO') . "\n";
    echo "  SHA1 match: " . (sha1($password) === $hash ? 'YES' : 'NO') . "\n";
    echo "  SHA256 match: " . (hash('sha256', $password) === $hash ? 'YES' : 'NO') . "\n";
    echo "  PASSWORD_VERIFY: " . (password_verify($password, $hash) ? 'YES' : 'NO') . "\n";
    echo "\n";
}
?>