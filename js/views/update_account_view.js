var app = app || {};

app.UpdateAccountView = Backbone.View.extend({

  el: "#container",

  template: "#update-view",

  events: {
    'click #edit': 'edit',
    'click #cancel': 'cancel',
    'click #save': 'save'
  },

  initialize: function() {
    this.$el.empty();
    this.render();
  },

  render: function() {
    var template = app.TemplateCache.get(this.template);
    var html = template(app.user.toJSON());
    this.$el.prepend(html).fadeIn(350)
    .css('margin-left', 'auto'); //center align content
    $('.edit-data').hide();
    $('#editSC').hide();
  },

  /* This will bring up the edit options for everything and
   * reset them to their current values in app.user.
   * This was just a bit easier code-wise than editting one by one.
   * The user can change anything, even password. They just use
   * the old password when confirming changes
   */
  edit: function(event) {
    event.preventDefault();
    // hide all the static data, show edit fields.
    $('#edit').hide();
    $('#editSC').show();
    $('.current-data').hide();
    $('.edit-data').show();
    
    // reset data in the input fields, just for safety
    $('#fname-input').val(app.user.get('firstName'));
    $('#lname-input').val(app.user.get('lastName'));
    $('#email-input').val(app.user.get('email'));
    $('#major-input').val(app.user.get('major'));
    $('#classes-input').tagit();
    classes = app.user.get('classes');
    for (c in classes) {
      console.log(classes[c]);
      $('#classes-input').tagit('createTag', classes[c]);
    }
    $('#year-input').val(app.user.get('grad_year'));
    $('#bio-input').val(app.user.get('bio'));
  },

  /* This will take all of the data from the document and bundle it in a JSON packet.
   * Then it asks for user password and sends everything to the server
   */
  save: function(event) {
    event.preventDefault();
    bootbox.prompt("Enter password to save your changes. If you changed your password, enter your old password.", function(result) {
      if (result !== null) {
        // PUT LOGIC HERE TO HANDLE THE GET REQUEST
      }
    });
    // little bit of a cheeky hack to make the prompt input take a password field instead of straight text.
    $('.bootbox-input-text').attr('type', 'password');
  },

  // cancel the edit
  cancel: function(event) {
    event.preventDefault();
    $('#editSC').hide();
    $('#edit').show();
    $('.edit-data').hide();
    $('.current-data').show();
    
    // reset data in the input fields
    $('#fname-input').val(app.user.get('firstName'));
    $('#lname-input').val(app.user.get('lastName'));
    $('#email-input').val(app.user.get('email'));
    $('#major-input').val(app.user.get('major'));
    $('#year-input').val(app.user.get('grad_year'));
    $('#bio-input').val(app.user.get('bio'));
  }
});
