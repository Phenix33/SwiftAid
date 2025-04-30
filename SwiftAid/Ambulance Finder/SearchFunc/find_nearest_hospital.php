<?php
$host = "localhost"; 
$user = "root"; 
$password = "new_password"; 
$dbname = "ambu_finder"; 

$conn = new mysqli($host, $user, $password, $dbname);

if ($conn->connect_error) {
    die(json_encode(["success" => false, "message" => "Database connection failed"]));
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $latitude = isset($_POST["latitude"]) ? floatval($_POST["latitude"]) : 0;
    $longitude = isset($_POST["longitude"]) ? floatval($_POST["longitude"]) : 0;

    if ($latitude == 0 || $longitude == 0) {
        echo json_encode(["success" => false, "message" => "Invalid coordinates"]);
        exit;
    }

    $query = "SELECT facility_name, latitude, longitude, 
              (6371 * ACOS(COS(RADIANS(?)) * COS(RADIANS(latitude)) * 
              COS(RADIANS(longitude) - RADIANS(?)) + 
              SIN(RADIANS(?)) * SIN(RADIANS(latitude)))) AS distance 
              FROM healthcare_facilities 
              ORDER BY distance 
              LIMIT 1";

    $stmt = $conn->prepare($query);
    $stmt->bind_param("ddd", $latitude, $longitude, $latitude);
    $stmt->execute();
    $stmt->bind_result($name, $lat, $lon, $distance);
    $stmt->fetch();
    $stmt->close();

    if ($name) {
        echo json_encode(["success" => true, "name" => $name, "distance" => round($distance, 2)]);
    } else {
        echo json_encode(["success" => false, "message" => "No hospitals found"]);
    }
}

$conn->close();
?>
