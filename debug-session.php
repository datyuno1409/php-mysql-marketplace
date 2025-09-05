<?php
session_start();

echo "Session Debug\n";
echo "=============\n";
echo "Session ID: " . session_id() . "\n";
echo "Session data: " . print_r($_SESSION, true) . "\n";

if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    echo "Login attempt:\n";
    echo "Username: $username\n";
    echo "Password: $password\n";
    
    if ($username === 'user' && $password === 'Fpt1409!@') {
        $_SESSION['loggedin'] = true;
        $_SESSION['username'] = $username;
        $_SESSION['id'] = 3;
        $_SESSION['role'] = 'user';
        
        echo "Session set successfully!\n";
        echo "New session data: " . print_r($_SESSION, true) . "\n";
    } else {
        echo "Invalid credentials\n";
    }
}

if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true) {
    echo "User is logged in!\n";
    echo "Redirecting to main page...\n";
    header("Location: /");
    exit;
}
?>

<form method="post">
    <input type="text" name="username" placeholder="Username" value="user">
    <input type="password" name="password" placeholder="Password" value="Fpt1409!@">
    <button type="submit">Login</button>
</form>
