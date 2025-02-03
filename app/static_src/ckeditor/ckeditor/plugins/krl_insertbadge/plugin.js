CKEDITOR.plugins.add('krl_insertbadge', {
    icons: 'krl_insertbadge',
    init: function(editor) {
        editor.addCommand('insertBadge', {
            exec: function(editor) {
                var element = editor.document.createElement('span');
                element.setAttribute('class', 'badge badge-secondary bg-secondary');
                element.setText('1.');
                editor.insertElement(element);
                editor.insertText('\u00A0');
            }
        });
        editor.ui.addButton('InsertBadge', {
            label: 'Insert Badge',
            command: 'insertBadge',
            toolbar: 'insert',
            icon: this.path + 'icons/insertbadge.png'  
        });
    }
});
