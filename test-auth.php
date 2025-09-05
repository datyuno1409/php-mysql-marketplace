<?php
include 'config.php';

$db = new Database();

echo "Testing authentication...\n";

$username = 'user';
$password = 'Fpt1409!@';

echo "Username: $username\n";
echo "Password: $password\n";

$result = $db->authenticate($username, $password, 'accounts');

if ($result) {
    echo "✅ Authentication successful!\n";
    echo "User data:\n";
    print_r($result[0]);
    
    $user = $result[0];
    echo "Role: " . $user['role'] . "\n";
    echo "ID: " . $user['id'] . "\n";
} else {
    echo "❌ Authentication failed!\n";
}
?>
