/**
 * CKEditor 5 replacement for the old krl_insertbadge plugin:
 * inserts <span class="badge badge-secondary bg-secondary">1.</span>&nbsp;
 */
(function () {
  var BADGE_HTML =
    '<span class="badge badge-secondary bg-secondary">1.</span>&nbsp;';
  var enhanced = Object.create(null);

  function insertBadge(editor) {
    var viewFragment = editor.data.processor.toView(BADGE_HTML);
    var modelFragment = editor.data.toModel(viewFragment);
    editor.model.insertContent(modelFragment);
    editor.editing.view.focus();
  }

  function enhance(id, editor) {
    if (enhanced[id]) {
      return;
    }
    var el = document.getElementById(id);
    if (!el || !el.parentNode) {
      return;
    }
    enhanced[id] = true;

    var bar = document.createElement("div");
    bar.className = "krl-ck5-badge-bar";
    bar.style.margin = "0 0 0.35rem 0";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "button";
    btn.textContent = "Insert Badge";
    btn.title = "Insert numbered badge (1.)";
    btn.addEventListener("click", function (event) {
      event.preventDefault();
      insertBadge(editor);
    });

    bar.appendChild(btn);
    el.parentNode.insertBefore(bar, el);
  }

  function scan() {
    var editors = window.editors || {};
    Object.keys(editors).forEach(function (id) {
      enhance(id, editors[id]);
    });
  }

  setInterval(scan, 500);
  document.addEventListener("DOMContentLoaded", scan);
})();
