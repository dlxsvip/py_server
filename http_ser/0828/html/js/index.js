/**
 * Created by wb-yyl187231 on 2016/8/24.
 */


$(function () {
    $.ajax({
        url: '../lib/file',
        dataType: 'text',
        success: function (data) {
            var arr = data.split('\n');
            //console.log(arr)
            //$("#file_list").html(arr) ;
            for (var n in arr) {
                if (arr[n].length > 0) {
                    $("#file_list").append("<div id='file' >" + arr[n] + "</div>");
                    //console.log("<div id='file' >" + arr[n] + "</div>")
                }

            }

            div_click();
            //div_mouse_enter();
            div_mouse_over();
        }
    });


})

// 鼠标单击事件
function div_click() {
    // 遍历id = file 的 div 添加点击事件
    $("div[id='file']").each(function () {
        $(this).click(function () {
            open_uri($(this).text())
        });
    });
}

// 鼠标指针穿过,离开元素时
function div_mouse_enter() {
    var arrImg = [".jpg", ".png"];
    var arrTxt = [".txt", ".md"];

    $("div[id='file']").each(function () {
        var name = $(this).text();
        //文件后缀
        var suffix = name.substring(name.lastIndexOf("."), name.length).toLocaleLowerCase();
        $(this).mouseenter(function () {
            // 通用事件
            $(this).addClass("div_file");

            if (!$(this).is(":animated")) {
                if (arrImg.indexOf(suffix) > -1) {
                    // 图片事件
                    setTimeout(show_img($(this).text()), 1000)
                } else if (arrTxt.indexOf(suffix) > -1) {
                    // 文本事件
                    show_txt($(this).text());
                }
            }
        }).mouseleave(function () {
            $(this).removeClass("div_file");
            close_img($(this).text());
            close_txt($(this).text());
        });
    });
}

// 鼠标指针离开元素时
function div_mouse_over() {
    var arrImg = [".jpg", ".png"];
    var arrTxt = [".txt", ".md"];
    // 给 id = file 的 div
    $("div[id='file']").each(function () {
        var me = $(this);
        var name = me.text();
        var suffix = name.substring(name.lastIndexOf("."), name.length).toLocaleLowerCase();
        var tmp_n;

        me.on({
            "mouseenter": function () {
                me.addClass("div_file");
                if (arrImg.indexOf(suffix) > -1) {
                    clearTimeout(tmp_n);
                    tmp_n = setTimeout(function(){
                        show_img(name)
                    }, 500);
                } else if (arrTxt.indexOf(suffix) > -1) {
                    show_txt(name);
                }
            },
            "mouseleave": function () {
                me.removeClass("div_file");
                clearTimeout(tmp_n);
                close_img(name);
                close_txt(name);
            }
        });

    });
}

function open_uri(uri) {
    //console.log(window.location.host)
    window.open("http://" + window.location.host + uri);
}

// 预览服务端 图片
function show_img(uri) {
    var url = "http://" + window.location.host + uri;
    $("#img-pre").slideDown(500);
    $("#imgPre").attr("src", url);
    //$("#img-pre").fadeIn(500);
}

function close_img() {
    $("#img-pre").slideUp(200);
    //$("#img-pre").fadeOut(100);
}

// 预览 文本
function show_txt(uri) {
    var url = "http://" + window.location.host + uri;
    $.ajax({
        type: "GET",
        url: url,
        beforeSend: function (request) {
            request.setRequestHeader("test", "yyl");
        },
        success: function (result) {
            $("#txt-pre").fadeIn(100);
            $("#txt-pre-area").val(result);
        }
    });
}

function close_txt() {
    $("#txt-pre").fadeOut(100);
}