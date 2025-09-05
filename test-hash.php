<?php
include 'config.php';

$db = new Database();

echo "Testing password hash...\n";

$password = "Fpt1409!@";
$hashed = $db->hashPassword($password);

echo "Password: $password\n";
echo "Hashed: $hashed\n";

// Check if this matches database
$expected_hash = "7fdaa4b045c8ff402b4459e51a2583072782eae0705b48c42998913bbf183301";
echo "Expected: $expected_hash\n";

if ($hashed === $expected_hash) {
    echo "✅ Hash matches!\n";
} else {
    echo "❌ Hash does not match!\n";
}

// Test authentication
echo "\nTesting authentication...\n";
$result = $db->authenticate("user", "Fpt1409!@", "accounts");
if ($result) {
    echo "✅ Authentication successful!\n";
    print_r($result[0]);
} else {
    echo "❌ Authentication failed!\n";
}
?>
