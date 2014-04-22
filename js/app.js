var app = app || {};

app.user = new app.User();
app.router = new app.Router();

Backbone.sync = function(method, model, options) {
  if (method === 'create') { // HTTP POST
    if (model instanceof app.Card) {
      $.ajax({
        type: 'POST',
        url: app.Deck.url,
        data: model.toJSON(),
        success: function(data) {},
        fail: function(data) {}
      });
    } else if (model instanceof app.User) {
    
    }
  } else if (method === 'read') { // HTTP GET
    if (model instanceof app.Card) {
    
    } else if (model instanceof app.User) {
    
    }
  } else if (method === 'update') { // HTTP PUT
    if (model instanceof app.Card) {
    
    } else if (model instanceof app.User) {
    
    }
  } else if (method === 'delete') { // HTTP DELETE
    if (model instanceof app.Card) {
    
    } else if (model instanceof app.User) {
    
    }
  }
}

app.TemplateCache = {
  get: function(selector) {
    if (!this.templates) {
      this.templates = {};
    }

    var template = this.templates[selector];
    if (!template) {
      var tmpl = $(selector).html();
      template = _.template(tmpl);
      this.templates[selector] = template;
    }

    return template;
  } 
};

$(function() {
  new app.AppView();
  Backbone.history.start();
});
