<?php
session_start();

echo "Session Test\n";
echo "============\n";
echo "Session ID: " . session_id() . "\n";
echo "Session save path: " . session_save_path() . "\n";

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
