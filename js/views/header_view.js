var app = app || {};

app.HeaderView = Backbone.View.extend({
  el: ".navbar-form",

  loginTemplate: "#login_header",
  logoutTemplate: "#logout_header",

  initialize: function() {
    this.listenTo(app.user, "change", this.render);
    this.render();
  },

  render: function() {
    var localUser = localStorage.getItem('deku'),
        template,
        html;
    if (localUser !== null) {
      template = app.TemplateCache.get(this.logoutTemplate);
      html = template(app.user.toJSON());
      this.$el.html(html);
    } else {
      template = app.TemplateCache.get(this.loginTemplate);
      this.$el.html(template);
    }
  }
});
