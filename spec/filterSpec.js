describe("A filter has a few basic elements.", function() {
  var filter = new app.Filter();
  it("Should have a filter attribute.", function() {
    expect(filter.get("filter")).toBe("");
  });

  it("Should have a field attribute.", function() {
    expect(filter.get("field")).toBe("");
  });
});
