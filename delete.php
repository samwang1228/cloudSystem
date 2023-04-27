
<?php

$dirname = $_POST['folder_name'];

$dirPath = "/share/".$dirname."/";

$cmd = "rm -r $dirPath";

shell_exec($cmd);

?>