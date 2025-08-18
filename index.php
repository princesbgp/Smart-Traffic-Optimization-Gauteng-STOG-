<?php
$page_title = "AI Traffic Optimizer";
$features = [
    ["Traffic Prediction", "Uses AI to predict congestion"],
    ["Route Optimization", "Finds fastest delivery paths"],
    ["Live Tracking", "Real-time GPS updates"]
];
?>
<!DOCTYPE html>
<html>
<head>
    <title><?php echo $page_title; ?></title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <header>
        <h1>AI Traffic Optimization</h1>
    </header>
    <div class="features">
        <?php foreach ($features as $feature): ?>
        <div class="feature-card">
            <h3><?php echo $feature[0]; ?></h3>
            <p><?php echo $feature[1]; ?></p>
        </div>
        <?php endforeach; ?>
    </div>
    <a href="contact.php" class="btn">Request Demo</a>
</body>
</html>
