var app = app || {};

app.User = Backbone.Model.extend({
    defaults: {
        firstName: "",
         lastName: "",
            email: ""
    }
});
