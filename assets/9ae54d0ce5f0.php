<!DOCTYPE html>
<meta charset="UTF-8">
<html>
<head>

<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" />
<title>Welcome! - The Mathematics Genealogy Project</title>
<style type="text/css"> 
body  {
	margin: 0; /* it's good practice to zero the margin and padding of the body element to account for differing browser defaults */
	padding: 0;
	text-align: center; /* this centers the container in IE 5* browsers. The text is then set to the left aligned default in the #container selector */
	color: #000000;
	font-family: Arial, Helvetica, sans-serif;
	font-size: 100%;
	background-color: #5E8059;
}
.twoColFixLtHdr #container {
	width: 780px;  /* using 20px less than a full 800px width allows for browser chrome and avoids a horizontal scroll bar */
	background: #FFFFFF; /* the auto margins (in conjunction with a width) center the page */
	border: 1px solid #000000;
	text-align: left; /* this overrides the text-align: center on the body element. */
	margin-top: 0;
	margin-right: auto;
	margin-bottom: 0;
	margin-left: auto;
} 
.twoColFixLtHdr #header {
	padding: 0 10px 0 20px;  /* this padding matches the left alignment of the elements in the divs that appear beneath it. If an image is used in the #header instead of text, you may want to remove the padding. */
	text-align: right;
	background-color: #CACC8F;
	height: 57px;
} 
.twoColFixLtHdr #header h1 {
	margin: 0; /* zeroing the margin of the last element in the #header div will avoid margin collapse - an unexplainable space between divs. If the div has a border around it, this is not necessary as that also avoids the margin collapse */
	padding: 10px 0; /* using padding instead of margin will allow you to keep the element away from the edges of the div */
}

.twoColFixLtHdr #main-tile { background: #8BBC83; }
.twoColFixLtHdr #column-tile { padding-right: 550px; background: white; width: 180px }
.twoColFixLtHdr #sidebar1 {
	float: left; /* since this element is floated, a width must be given */
	width: 160px; /* the background color will be displayed for the length of the content in the column, but no further */
	padding: 15px 10px 15px 10px;
	background: #8BBC83;
	font-size: small;
	text-align: center;
}
   .twoColFixLtHdr #sidebar1 p a:link {
 color: navy;
    }
.twoColFixLtHdr #mainContent { 
  float: left;
 width: 600px;
  margin-right: -600px;
 position: relative;


} 
   .twoColFixLtHdr #paddingWrapper {
      padding: 5px 20px;
	}
.twoColFixLtHdr #footer {
	padding: 10px 10px 0 10px;
	text-align: center;
	font-size: small;
	font-weight: normal;
	background-color: #CACC8F;
} 
.clearfix:after {
    content: "."; 
    display: block; 
    height: 0; 
    clear: both; 
    visibility: hidden;
}

.clearfix {display: inline-table;}


.twoColFixLtHdr #footer p {
	margin: 0; /* zeroing the margins of the first element in the footer will avoid the possibility of margin collapse - a space between divs */
	padding: 10px 0; /* padding on this element will create space, just as the the margin would have, without the margin collapse issue */
}
.fltrt { /* this class can be used to float an element right in your page. The floated element must precede the element it should be next to on the page. */
	float: right;
	margin-left: 8px;
}
.fltlft { /* this class can be used to float an element left in your page */
	float: left;
	margin-right: 8px;
}
.clearfloat { /* this class should be placed on a div or break element and should be the final element before the close of a container that should fully contain a float */
	clear:both;
    height:0;
    font-size: 1px;
    line-height: 0px;
}
th {
    text-align: center;
}

</style>
<!--[if IE 5]>
<style type="text/css"> 
/* place css box model fixes for IE 5* in this conditional comment */
.twoColFixLtHdr #sidebar1 { width: 190px; }
</style>
<![endif]--><!--[if IE]>
<style type="text/css"> 
/* place css fixes for all versions of IE in this conditional comment */
.twoColFixLtHdr #sidebar1 { padding-top: 30px; }
.twoColFixLtHdr #mainContent { zoom: 1; }
/* the above proprietary zoom property gives IE the hasLayout it needs to avoid several bugs */
</style>
<![endif]-->
<script src="SpryAssets/SpryMenuBar.js" type="text/javascript"></script>
<link href="SpryAssets/SpryMenuBarVertical.css" rel="stylesheet" type="text/css" />
<link href="SpryAssets/SpryMenuBarHorizontal.css" rel="stylesheet" type="text/css" />

<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<link rel="stylesheet" type="text/css" href="jquery-eu-cookie-law-popup.css"/>
<script src="jquery-eu-cookie-law-popup.js"></script>
  <script type="text/javascript"> 
window.onload = function() {
  document.getElementById( 'searchTerms' ).focus();
}
</script>

<script async src="https://www.googletagmanager.com/gtag/js?id=UA-16329138-2"></script>
<script>
	 window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
// Don’t call the init functions just yet:
// gtag('js', new Date());
// gtag('config', 'UA-XXXXXXXX-1');

function initialiseGoogleAnalytics() {
	gtag('js', new Date());
	gtag('config', 'UA-16329138-2');
}

// Subscribe for the cookie consent events
$(document).bind("user_cookie_already_accepted", function(event, object) {
		initialiseGoogleAnalytics();
	});

$(document).bind("user_cookie_consent_changed", function(event, object) {
		const userConsentGiven = $(object).attr('consent');
		if (userConsentGiven) {
			// User clicked on enabling cookies. Now it's safe to call the
			// init functions.
			initialiseGoogleAnalytics();
		}
	});
</script>
</head>

<body class="twoColFixLtHdr eupopup eupopup-top">

<div id="container">
  <div id="header">
    <a href="index.php"><img src="images/tree-small.gif" alt="Tree" width="46" height="57" style="border: 0" class="fltlft" title="tree" /></a>
    <h1>Mathematics Genealogy Project</h1>
  <!-- end #header --></div>
  <div id="column-tile">
  <div id="main-tile" class="clearfix">
  <div id="sidebar1">
    <ul id="MenuBar1" class="MenuBarVertical">
      <li><a href="index.php">Home</a></li>
      <li><a href="search.php">Search</a></li>
      <li><a href="extrema.php">Extrema</a></li>
      <li><a href="about.php" class="MenuBarItemSubmenu">About MGP</a>
        <ul>
          <li><a href="mission.php">Mission</a></li>
	<li><a href="http://www.ams.org/notices/200708/tx070801002p.pdf">History (PDF)</a></li>
<li><a href="https://northdakotastate-ndus.nbsstore.net/mathematics-genealogy-project-donation">Support Us</a></li>
            <li><a href="news.php" title="Announcements">News</a></li>
            <li><a href="staff.php">Staff</a></li>
            <li><a href="recognition.php">Recognition</a></li>
            <li><a href="acknowledgments.php">Acknowledgments</a></li>
          </ul>
      </li>
      <li><a href="links.php">Links</a></li>
      <li><a href="faq.php" title="Frequently Asked Questions">FAQs</a></li>
      <li><a href="posters.php">Posters</a></li>
      <li><a href="submit.php">Submit Data</a></li>
      <li><a href="contact.php">Contact</a></li>
      <li><a href="https://northdakotastate-ndus.nbsstore.net/mathematics-genealogy-project-donation">Donate</a></li>
    </ul>

<p>A 
service of the <a href="https://www.ndsu.edu/">NDSU</a> <a href="https://www.ndsu.edu/math/">Department of Mathematics</a>, in association with the <a href="http://www.ams.org/">American Mathematical Society</a>.</p>

  <!-- end #sidebar1 --></div>
  <div id="mainContent"><div id="paddingWrapper">
   <!-- ImageReady Slices (genealogy_skeleton.ai) -->
<div style="width: 580px; margin-left: auto; margin-right: auto">





<img id="skeleton" src="images/genealogy_skeleton.png" width="580" height="334" style="border: 0" alt="Genealogy Tree Excerpt" usemap="#skeleton-map" />
<map id="skeleton-map" name="skeleton-map">

<area  alt="Kaestner" title="" href="id.php?id=66476" shape="rect" coords="127,3,183,21" style="outline:none;" target="_self"     />
<area  alt="Thibaut" title="" href="id.php?id=57667" shape="rect" coords="68,59,126,76" style="outline:none;" target="_self"     />
<area  alt="Gudermann" title="" href="id.php?id=29458" shape="rect" coords="12,105,102,122" style="outline:none;" target="_self"     />
<area  alt="Weierstrass" title="" href="id.php?id=7486" shape="rect" coords="16,157,98,175" style="outline:none;" target="_self"     />
<area  alt="Kovalevskaya" title="" href="id.php?id=9711" shape="rect" coords="7,220,104,237" style="outline:none;" target="_self"     />
<area  alt="Dirksen" title="" href="id.php?id=41423" shape="rect" coords="117,109,177,123" style="outline:none;" target="_self"     />
<area  alt="Jacobi" title="" href="id.php?id=15635" shape="rect" coords="122,156,174,171" style="outline:none;" target="_self"     />
<area  alt="Gordan" title="" href="id.php?id=15654" shape="rect" coords="121,210,178,228" style="outline:none;" target="_self"     />
<area  alt="Noether" title="" href="id.php?id=6967" shape="rect" coords="122,268,179,281" style="outline:none;" target="_self"     />
<area  alt="Pfaff" title="" href="id.php?id=18230" shape="rect" coords="158,57,201,71" style="outline:none;" target="_self"     />
<area  alt="Gauss" title="" href="id.php?id=18231" shape="rect" coords="185,104,228,121" style="outline:none;" target="_self"     />
<area  alt="Gerling" title="" href="id.php?id=29642" shape="rect" coords="210,165,269,186" style="outline:none;" target="_self"     />
<area  alt="Pluecker" title="" href="id.php?id=7402" shape="rect" coords="249,199,307,220" style="outline:none;" target="_self"     />
<area  alt="Klein" title="" href="id.php?id=7401" shape="rect" coords="367,245,405,263" style="outline:none;" target="_self"     />
<area  alt="Lindemann" title="" href="id.php?id=7404" shape="rect" coords="302,272,383,290" style="outline:none;" target="_self"     />
<area  alt="Hilbert" title="" href="id.php?id=7298" shape="rect" coords="304,308,358,326" style="outline:none;" target="_self"     />
<area  alt="Furtwaengler" title="" href="id.php?id=7443" shape="rect" coords="400,273,489,291" style="outline:none;" target="_self"     />
<area  alt="Taussky-Todd" title="" href="id.php?id=11912" shape="rect" coords="397,310,486,328" style="outline:none;" target="_self"     />
<area  alt="Lipschitz" title="" href="id.php?id=19964" shape="rect" coords="395,212,459,227" style="outline:none;" target="_self"     />
<area  alt="Dirichlet" title="" href="id.php?id=17946" shape="rect" coords="416,157,483,172" style="outline:none;" target="_self"     />
<area  alt="Fourier" title="" href="id.php?id=17981" shape="rect" coords="382,101,434,117" style="outline:none;" target="_self"     />
<area  alt="Poisson" title="" href="id.php?id=17865" shape="rect" coords="484,100,536,116" style="outline:none;" target="_self"     />
<area  alt="Lagrange" title="" href="id.php?id=17864" shape="rect" coords="432,68,499,85" style="outline:none;" target="_self"     />
<area  alt="Laplace" title="" href="id.php?id=108295" shape="rect" coords="520,65,576,84" style="outline:none;" target="_self"     />
<area  alt="Euler" title="" href="id.php?id=38586" shape="rect" coords="453,19,493,37" style="outline:none;" target="_self"     />
<area  alt="Moebius" title="" href="id.php?id=35953" shape="rect" coords="232,85,289,104" style="outline:none;" target="_self"     />
<area  alt="Dedekind" title="" href="id.php?id=18233" shape="rect" coords="226,120,293,138" style="outline:none;" target="_self"     />
</map>

  </div>
<form action="quickSearch.php" method="post"> <div style="text-align: center"><label for="searchTerms">Quick Search</label> <input name="searchTerms" type="text" size="30" maxlength="90" id="searchTerms" /> <input name="Submit" type="submit" value="Search" />
 <br /><span style="font-size: small"><a href="search.php">Advanced Search</a></span></div></form>

<p style="text-align: center"><span style="font-size: x-large; color: red; font-style:  italic">334628  records as of 19 October 2025</span><br /><span style="font-size: small">View the <a href="growth_image.php">growth</a> of the genealogy project</span></p><div style="height: 12ex"> </div>

   <!-- InstanceEndEditable -->
</div><!-- end #paddingWrapper -->

  <!-- end #mainContent --></div>
	<!-- This clearing element should immediately follow the #mainContent div in order to force the #container div to contain all child floats -->
</div></div>	
  <div id="footer">
<ul id="MenuBar2" class="MenuBarHorizontal">
      <li><a href="search.php">Search</a>        </li>
      <li><a href="about.php" class="MenuBarItemSubmenu">About MGP</a>
          <ul>
            <li><a href="mission.php">Mission</a></li>
            <li><a href="news.php" title="Announcements">News</a></li>
            <li><a href="staff.php">Staff</a></li>
            <li><a href="recognition.php">Recognition</a></li>
            <li><a href="acknowledgments.php"><span style="font-size: x-small">Acknowledgments</span></a></li>
          </ul>
      </li>
      <li><a href="links.php">Links</a></li>
      <li><a href="faq.php" title="Frequently Asked Questions">FAQs</a></li>
      <li><a href="posters.php">Posters</a></li>
      <li><a href="submit.php">Submit Data</a></li>
      <li><a href="contact.php">Contact</a></li>
 
</ul>
<br />
<p>The Mathematics Genealogy Project is in need of funds 
to help pay for student help and other associated costs. If you would like to 
contribute, please <a href="https://northdakotastate-ndus.nbsstore.net/mathematics-genealogy-project-donation">donate online</a> using credit card or bank transfer or mail  your tax-deductible contribution to:</p>

<p>
Mathematics Genealogy Project<br /> 
Department of Mathematics<br />
North Dakota State University<br />
P. O. Box 6050<br />
  Fargo, North Dakota 58108-6050</p>

</div>
<!-- end #container --></div>
<script type="text/javascript">
var MenuBar1 = new Spry.Widget.MenuBar("MenuBar1", {imgRight:"SpryAssets/SpryMenuBarRightHover.gif"});
var MenuBar2 = new Spry.Widget.MenuBar("MenuBar2", {imgDown:"SpryAssets/SpryMenuBarDownHover.gif", imgRight:"SpryAssets/SpryMenuBarRightHover.gif"});
</script>

</body>
<!-- InstanceEnd --></html>
