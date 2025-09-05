<?php
include 'config.php';

$db = new Database();

echo "Testing simple login...\n";

// Test direct database query
$result = $db->select('accounts', '*', "WHERE username = 'user'");
if ($result) {
    echo "User found: " . $result[0]['username'] . "\n";
    echo "Password in DB: " . $result[0]['password'] . "\n";
    echo "Password length: " . strlen($result[0]['password']) . "\n";
    
    // Test authentication
    $auth_result = $db->authenticate('user', 'Fpt1409!@', 'accounts');
    if ($auth_result) {
        echo "✅ Authentication successful!\n";
    } else {
        echo "❌ Authentication failed!\n";
    }
} else {
    echo "❌ User not found!\n";
}
?>
