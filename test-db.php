<?php
include 'config.php';

$db = new Database();

echo "Testing database connection...\n";

// Test products
$products = $db->select('products', '*', 'LIMIT 3');
echo "Products found: " . count($products) . "\n";

if (count($products) > 0) {
    echo "First product: " . $products[0]['name'] . "\n";
}

// Test categories
$categories = $db->select('categories', '*');
echo "Categories found: " . count($categories) . "\n";

if (count($categories) > 0) {
    echo "First category: " . $categories[0]['category_name'] . "\n";
}

echo "Database test completed!\n";
?>
