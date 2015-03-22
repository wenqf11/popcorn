/**
 * Created with PyCharm.
 * User: LY
 * Date: 15-3-22
 * Time: 下午9:02
 * To change this template use File | Settings | File Templates.
 */
var containerHeight = document.getElementById("container").scrollHeight;
var footer = document.getElementsByTagName("footer");
var allHeight = document.documentElement.clientHeight;
if(containerHeight < allHeight){
    footer[0].style.position = "absolute";
    footer[0].style.bottom = "0px";
}
else{
    footer[0].style.position = "";
    footer[0].style.bottom = "";
}
