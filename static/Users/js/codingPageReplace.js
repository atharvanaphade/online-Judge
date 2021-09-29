if ('{{ code }}' != '') {
    var json_code = `{{ code }}`;
    console.log(typeof json_code);
    console.log(json_code);
    var code = json_code.replace(/&amp;/g, "&");
    code = code.replace(/&lt;/g, "<");
    code = code.replace(/&gt;/g, ">");
    code = code.replace(/&quot;/g, '"');
    code = code.replace(/&#39;/g, "'");
    code = code.replace(/&#x2F;/g, "/");
    code = code.replace(/&#x60;/g, "`");
    code = code.replace(/&#x3D;/g, "=");
    code = code.slice(1, -1);
    console.log(code);
    editor.setValue(code);
}