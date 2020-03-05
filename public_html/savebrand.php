<?php
  $firstname = $_POST['firstname'];
  $lastname = $_POST['lastname'];
  $email = $_POST['email'];
  $phone = $_POST['phone'];
  $company = $_POST['company'];
  $businesstype = $_POST['businesstype'];
  $website = $_POST['website'];
  $instagram = $_POST['instagram'];
  $message = $_POST['message'];

  require "includes/dbconnect.php";
  $conn = new mysqli($database_host, $database_username, $database_password, $database_name);
  if ($conn -> connect_error) {
    die($conn -> connect_error);
  }
  else{
    $query = "insert into Brandally (firstname, lastname, email, phone, company, businesstype, website, instagram, message) values('$firstname', '$lastname', '$email', '$phone', '$company', '$businesstype', '$website', '$instagram', '$message')";
    $result = $conn -> query($query);
    if ($result){
      header('Location: /thankyou.html');
    }
    else {
      echo('Registration Failed ' . $conn -> error);
    }
  }

 ?>
