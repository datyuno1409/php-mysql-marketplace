<?php
session_start();

echo "Login Debug\n";
echo "===========\n";
echo "Session ID: " . session_id() . "\n";
echo "Session data before: " . print_r($_SESSION, true) . "\n";

if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    echo "Login attempt:\n";
    echo "Username: $username\n";
    echo "Password: $password\n";
    
    // Simulate user data
    $userData = [
        'id' => 3,
        'name' => 'Test User',
        'role' => 'user',
        'username' => $username
    ];
    
    $_SESSION['loggedin'] = true;
    $_SESSION['id'] = $userData['id'];
    $_SESSION['name'] = $userData['name'];
    $_SESSION['username'] = $userData['username'];
    $_SESSION['role'] = $userData['role'];
    
    echo "Session data after: " . print_r($_SESSION, true) . "\n";
    
    echo "Redirecting to main page...\n";
    header("Location: /");
    exit;
}

if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true) {
    echo "User is logged in!\n";
    echo "Session data: " . print_r($_SESSION, true) . "\n";
    echo "Redirecting to main page...\n";
    header("Location: /");
    exit;
}
?>

<form method="post">
    <input type="text" name="username" placeholder="Username" value="user">
    <input type="password" name="password" placeholder="Password" value="anything">
    <button type="submit">Login</button>
</form>
