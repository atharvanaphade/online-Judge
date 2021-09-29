function myfunc() {
    var lang = document.getElementById('lang').value;
    if (lang === 'python') this.editor.setOption('mode', 'python');
    else this.editor.setOption('mode', 'clike');
}

var editor = CodeMirror(document.querySelector('.editor-wrapper'), {
    lineNumbers: true,
    tabSize: 2,
    mode: 'clike',
    theme: 'base16-dark',
    styleActiveLine: true,
    autoCloseBrackets: true,
    matchBrackets: true,
});