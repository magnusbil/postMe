<?php
  header("Access-Control-Allow-Origin: http://sae.magnusb.net");
  //header("Access-Control-Allow-Headers: X-Requested-With");
  header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
  header("Access-Control-Request-Method: POST");

  /*
  //database information
	$servername = "magnusb.net";
	$dbUN="magnus";
	$dbPass="N3crotyper!";
	$dbName = "sae";
	$connect = null;

	//user input
  $data = json_decode(file_get_contents('php://input'), true);
	$username = $data['username'];
	$password = $data['password'];
	
	//user object information
	$user['name']="";
	$user['posts']={};
	
	function handleRequest(){
		try{
			$connect = new PDO("mysql:host=$servername;dbname=$dbName", $dbUN, $dbPass);
			$connect->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);	
		}catch(PDOException $e){
			echo "Connection Failed: " . $e->getMessage(); 
		}
	}
	
	function tearDownRequest(){
		$connect = null;
	}

	function findUser(){
		$info = $connect->prepare('SELECT username, post FROM Users WHERE username="''" AND password="''" LIMIT 1');
		$info->execute();
		$res =$info->setFetchMode(PDO::FETCH_ASSOC);
		
		if(info.fetchAll() != null){
			$user['name']=info.fetchAll();
			return true;
		}
		return false;
	}
	
	function getUserInfo(){
		handleRequest();	

		$postC = $connect->prepare('SELECT postCount FROM Users WHERE username="'. $user['name'] .'" LIMIT 1');
		$postC->execute();
		$res = $postsC->setFetchMode(PDO::FETCH_ASSOC);
		$user['postCount'] = $postC.fetchAll();
			
		$posts = $connect->prepare('SELECT id, message fROM Posts WHERE userID="'. $user['name'] .'"');
		$posts->execute();
		$res = $posts->setFetchMode(PDO::FETCH_ASSOC);

		foreach($values->fetchAll() as $key => $value){
			$user['posts']['post'] = $value; 
		}
		
		return $user;
	}

	function sign_in(){
		if(findUser()){
			return getUserInfo();
		}
		else{ 
			return null;
		}
	}

	sign_in();*/
 
  return "script run successfully!";
?>
