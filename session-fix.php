<?php
// Set session save path before starting session
ini_set('session.save_path', '/var/lib/php/sessions');
ini_set('session.gc_maxlifetime', 1440);
ini_set('session.cookie_lifetime', 0);
ini_set('session.use_cookies', 1);
ini_set('session.use_only_cookies', 1);
ini_set('session.cookie_httponly', 1);

session_start();

echo "Session Configuration Test\n";
echo "=========================\n";
echo "Session ID: " . session_id() . "\n";
echo "Session save path: " . ini_get('session.save_path') . "\n";
echo "Session directory exists: " . (is_dir(ini_get('session.save_path')) ? 'YES' : 'NO') . "\n";
echo "Session directory writable: " . (is_writable(ini_get('session.save_path')) ? 'YES' : 'NO') . "\n";

if (isset($_POST['test'])) {
    $_SESSION['test'] = 'Hello World';
    $_SESSION['loggedin'] = true;
    $_SESSION['username'] = 'testuser';
    $_SESSION['role'] = 'user';
    
    echo "Session data set!\n";
    echo "Redirecting...\n";
    header("Location: " . $_SERVER['PHP_SELF']);
    exit;
}

echo "Session data:\n";
print_r($_SESSION);

if (isset($_SESSION['test'])) {
    echo "✅ Session is working!\n";
} else {
    echo "❌ Session not working\n";
}
?>

<form method="post">
    <button type="submit" name="test">Test Session</button>
</form>
