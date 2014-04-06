var app = app || {};

app.HeaderView = Backbone.View.extend({
    el: ".navbar-form",

    template: _.template( $('#login_header').html() ),

    initialize: function() {
        this.listenTo(app.user, "change", this.render);
        this.render();
    },

    render: function() {
        if (app.user.get("firstName") !== "") {
            this.template = _.template( $('#logout_header').html() );
            this.$el.html(this.template(app.user.toJSON()));
        } else {
            this.template = _.template( $('#login_header').html() );
            this.$el.html(this.template);
        }
    },

    alertToChange: function() {
        console.log("The user's name has changed to " + app.user.get("firstName"));
    }

})
