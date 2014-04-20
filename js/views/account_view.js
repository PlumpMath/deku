var app = app || {};

app.AccountView = Backbone.View.extend({

	el: "#my-account",

  events: {
    'click #update-account': "update"
  },

  template: "#account-view",

	initialize: function() {
		this.render();
	},

	render: function() {
    var template = app.TemplateCache.get(this.template);
		var html = template(app.user.toJSON());
    this.$el.html(html);
	},

  update: function(event) {
    event.preventDefault();
    profile = (app.user.get('firstName') + "_" + app.user.get('lastName')).split(' ');
    route = '';
    // if someone's name has many spaces, this will replace spaces with '_'
    for (p in profile) {
      route += (profile[p] += '_');
    }
    route = route.substring(0, route.length - 1); //chop off the last '_'
    app.router.navigate('update/' + route + '/' + app.user.get('id'), {trigger: true});
  }

});
