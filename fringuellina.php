<?php
//echo 'Its been a while since ive done php. Let me hide my gun first.';

class Fringuellina {
	public static $cakeRecipeName = "Cakes"; 

    public static function PrintPage(){
        // Multiple pages
		$pageInterval = 100;
		$from = (isset($_GET["from"])) ? $_GET["from"] : 999;
		$to = $from+$pageInterval;
		$users = $GLOBALS['db']->fetchAll('SELECT * FROM users WHERE id >= ? AND id < ?', [$from, $to]);
		$groups = $GLOBALS["db"]->fetchAll("SELECT * FROM privileges_groups");

        // Print stuff
		echo '<div id="wrapper">';
		printAdminSidebar();
		echo '<div id="page-content-wrapper">';
		// Maintenance check
		P::MaintenanceStuff();
		// Print Success if set
		if (isset($_GET['s']) && !empty($_GET['s'])) {
			P::SuccessMessageStaccah($_GET['s']);
		}
		// Print Exception if set
		if (isset($_GET['e']) && !empty($_GET['e'])) {
			P::ExceptionMessageStaccah($_GET['e']);
        }
        
		// Get values
		//$wm = current($GLOBALS['db']->fetch("SELECT value_int FROM system_settings WHERE name = 'website_maintenance'"));
		
		echo '<p align="center"><font size=5><i class="fa fa-birthday-cake"></i>	Cakes</font></p><br>';
		// Quick edit/silence/kick user button
		echo '<div><p align="center"><button type="button" class="btn btn-primary" data-toggle="modal" data-target="#quickLookupUserModal">Quick lookup user (username)</button>';
		echo '&nbsp;&nbsp; <button type="button" class="btn btn-info" data-toggle="modal" data-target="#quickLookupUseridModal">Quick lookup user (user_id)</button>';
		echo '&nbsp;&nbsp; <button type="button" class="btn btn-warning" data-toggle="modal" data-target="#quickLookupScoreidModal">Quick lookup user (score_id)</button>';
		echo '</p>';
		// Users plays table
		echo '<table class="table table-striped table-hover table-50-center">
		<thead>
		<tr><th class="text-center"><i class="fa fa-user"></i>	ID</th><th class="text-center">Username</th><th class="text-center">Cakes</th><th class="text-center">Toppings found</th><th class="text-center">Flags found</th><th class="text-center">Status</th><th class="text-center">Actions</th></tr>
		</thead>
		<tbody>';
		foreach ($users as $user) {
			// Get allowed color/text
			$statusColor = "success";
			$statusText = "Ok";
			if (($user["privileges"] & Privileges::UserPublic) == 0 && ($user["privileges"] & Privileges::UserNormal) == 0) {
				// Not visible and not active, banned
				$statusColor = "danger";
				$statusText = "Banned";
			} else if (($user["privileges"] & Privileges::UserPublic) == 0 && ($user["privileges"] & Privileges::UserNormal) > 0) {
				// Not visible but active, restricted
				$statusColor = "warning";
				$statusText = "Restricted";
			} else if (($user["privileges"] & Privileges::UserPublic) > 0 && ($user["privileges"] & Privileges::UserNormal) == 0) {
				// Visible but not active, disabled (not supported yet)
				$statusColor = "default";
				$statusText = "Locked";
            }
            
            $cakes = current($GLOBALS['db']->fetch('SELECT COUNT(*) FROM cakes WHERE userid = ?', [$user["id"]]));

			$toppings = current($GLOBALS['db']->fetch('SELECT COUNT(*) FROM cakes WHERE userid = ? AND detected NOT LIKE ?', [$user["id"], '[]']));

			$flags = current($GLOBALS['db']->fetch('SELECT COUNT(*) FROM cakes WHERE userid = ? AND flags NOT IN (0,4)', [$user["id"]]));

			// Print row
			echo '<tr>';
			echo '<td><p class="text-center">'.$user['id'].'</p></td>';
			echo '<td><p class="text-center"><b>'.$user['username'].'</b></p></td>';
			echo '<td><p class="text-center">'.$cakes.'</p></td>';
			echo '<td><p class="text-center">'.$toppings.'</p></td>';
			echo '<td><p class="text-center">'.$flags.'</p></td>';
            echo '<td><p class="text-center"><span class="label label-'.$statusColor.'">'.$statusText.'</span></p></td>';
            echo '<td><p class="text-center"><div class="btn-group">';
			echo '<a title="Edit user" class="btn btn-xs btn-primary" href="index.php?p=128&id='.$user['id'].'"><span class="glyphicon glyphicon-pencil"></span></a>';
			if (hasPrivilege(Privileges::AdminBanUsers)) {
				if (isBanned($user["id"])) {
					echo '<a title="Unban user" class="btn btn-xs btn-success" onclick="sure(\'submit.php?action=banUnbanUser&id='.$user['id'].'\')"><span class="glyphicon glyphicon-thumbs-up"></span></a>';
				} else {
					echo '<a title="Ban user" class="btn btn-xs btn-warning" onclick="sure(\'submit.php?action=banUnbanUser&id='.$user['id'].'\')"><span class="glyphicon glyphicon-thumbs-down"></span></a>';
				}
				if (isRestricted($user["id"])) {
					echo '<a title="Remove restrictions" class="btn btn-xs btn-success" onclick="sure(\'submit.php?action=restrictUnrestrictUser&id='.$user['id'].'\')"><span class="glyphicon glyphicon-ok-circle"></span></a>';
				} else {
					echo '<a title="Restrict user" class="btn btn-xs btn-warning" onclick="sure(\'submit.php?action=restrictUnrestrictUser&id='.$user['id'].'\')"><span class="glyphicon glyphicon-remove-circle"></span></a>';
				}
			}
			echo '</div>';
			echo '</td>';
			echo '</tr>';
		}
		echo '</tbody></table>';
		echo '<p align="center"><a href="index.php?p=128&from='.($from-($pageInterval+1)).'">< Previous page</a> | <a href="index.php?p=128&from='.($to).'">Next page ></a></p>';
		echo '</div>';
    }

    public static function PrintInfoPage(){
		
    }

    public static function PrintCakesSummary(){
		// Print stuff
		echo '<div id="wrapper">';
		printAdminSidebar();
		echo '<div id="page-content-wrapper">';
		// Maintenance check
		P::MaintenanceStuff();
		// Print Success if set
		if (isset($_GET['s']) && !empty($_GET['s'])) {
			P::SuccessMessageStaccah($_GET['s']);
		}
		// Print Exception if set
		if (isset($_GET['e']) && !empty($_GET['e'])) {
			P::ExceptionMessageStaccah($_GET['e']);
        }
    }

    public static function PrintEditCake(){

    }

    public static function RAPButton(){
		echo '<li><a href="index.php?p=128"><i class="fa fa-birthday-cake"></i>	Cakes</a></li>';
    }

    public static function RAPCakesListButton(){
		echo '<li><a href="index.php?p=130"><i class="fa fa-book"></i>	Cake recipes</a></li>';
    }

    public static function ToggleCake(){

    }

	public static function RemoveCake(){

    }

    public static function EditCake(){

	}
}
?>