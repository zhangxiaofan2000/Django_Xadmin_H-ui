$(document).ready(function () {
    //用户注册
    $("#register").click(function () {
        window.location.href = "index.html";
    });
    //刷新验证码
    $("#refresh_vcode").click(function () {
        $("#refresh_vcode").attr('src', "https://jkdev.cn/show_code.php");
    });
});