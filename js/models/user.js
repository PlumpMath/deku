var app = app || {};

app.User = Backbone.Model.extend({
    defaults: {
        firstName: "User",
        lastName: "Name",
        email: "userName@umbc.edu",
        university: "UMBC",
        bio: "I love programming!",
        classes: ["CMSC345"],
        grad_year: "2015",
        major: "CMSC"
    }
});
