describe("A user should have several attributes.", function() {
  var user = new app.User();

  it("Should have an id.", function() {
    expect(user.get("id")).toBe(-1);
  });

  it("Should have a first name.", function() {
    expect(user.get("firstName")).toBe("");
  });

  it("Should have a last name.", function() {
    expect(user.get("lastName")).toBe("");
  });

  it("Should have a email.", function() {
    expect(user.get("email")).toBe("");
  });

  it("Should have a university.", function() {
    expect(user.get("university")).toBe("");
  });

  it("Should have an empty biography.", function() {
    expect(user.get("bio")).toBe("");
  });

  it("Should have an empty 'classes' array.", function() {
    var classes = user.get("classes");
    expect(classes instanceof Array).toBe(true);
    expect(classes.length).toBe(0);
  });

  it("Should have a graduation year.", function() {
    expect(user.get("grad_year")).toBe("");
  });

  it("Should have a major.", function() {
    expect(user.get("major")).toBe("");
  });        

});
