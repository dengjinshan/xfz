var gulp = require("gulp");
var cssnano = require("gulp-cssnano");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");
var concat = require("gulp-concat");
var cache = require("gulp-cache");
var imagemin = require("gulp-imagemin");
var bs = require("browser-sync").create();
var sass = require("gulp-sass");
var sourcemaps = require("gulp-sourcemaps");

var path = {
    'html': './templates/**/',
    'css': './src/css/**/',
    'js': './src/js/',
    'image': './src/image',
    'css_dist': './dist/css/',
    'js_dist': './dist/js',
    'images_dist': './dist/images'
};

//定义处理html文件的任务
gulp.task("html",function () {
    gulp.src(path.html + '*.html')
        .pipe(bs.stream())  // 执行重新加载文件任务
})

// 定义一个css的任务
gulp.task("css",function () {  //定义一个压缩文件的任务
    return gulp.src(path.css + '*.scss')  //被压缩的scss文件的路径
        .pipe(sass().on("error",sass.logError))
        .pipe(cssnano())  //压缩任务
        .pipe(rename({"suffix":".min"}))  //重命名
        .pipe(gulp.dest(path.css_dist))  //压缩后存放的路径
        .pipe(bs.stream())  //重新加载
});

//定义一个处理js文件的任务
gulp.task("js",function () {
    gulp.src(path.js + '*.js')
        .pipe(sourcemaps.init())  //会自动检测网页出现的错误，并显示
        .pipe(uglify())
        .pipe(rename({"suffix":".min"}))
        .pipe(sourcemaps.write())  //显示错误
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
});

//定义一个处理图片的任务
gulp.task("images",function () {
    gulp.src(path.images + '*.*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.images_dist))
        .pipe(bs.stream())
});

//定义监听文件修改的任务
gulp.task("watch",function () {
    gulp.watch(path.html + '*.html', ['html']);
    gulp.watch(path.css + '*.scss', ['css']);  //监听 文件路径 监听后执行的任务
    gulp.watch(path.js + '*.js', ['js']);
    gulp.watch(path.images + '*.*', ['images']);
});

//初始化browser-sync的任务
gulp.task("bs",function () {
    bs.init({
        'server': {
            'baseDir': './'     //指定任务参数
        }
    })
});

//创建一个默认的任务
gulp.task("default", ['bs', 'watch']);  //任务名，【执行后执行的任务】
