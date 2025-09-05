<?php
include 'config.php';

$db = new Database();

echo "Debug Authentication\n";
echo "===================\n";

$username = 'user';
$password = 'Fpt1409!@';

echo "Username: $username\n";
echo "Password: $password\n";

// Test hash function
$hashed = $db->hashPassword($password);
echo "Hashed password: $hashed\n";

// Test database query directly
$result = $db->select('accounts', '*', "WHERE username = '$username'");
echo "Direct query result:\n";
print_r($result);

if ($result) {
    $user = $result[0];
    echo "User password in DB: " . $user['password'] . "\n";
    echo "Password match: " . ($user['password'] === $hashed ? 'YES' : 'NO') . "\n";
    
    // Test authentication step by step
    $username_clean = $db->validate($username);
    echo "Cleaned username: $username_clean\n";
    
    $condition = "WHERE username = '$username_clean' AND password = '$hashed'";
    echo "SQL condition: $condition\n";
    
    $auth_result = $db->select('accounts', '*', $condition);
    echo "Auth query result:\n";
    print_r($auth_result);
}
?>
