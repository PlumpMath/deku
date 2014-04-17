describe("A card should have a several attributes...", function() {
  var card = new app.Card();
  it("Should have a category.", function() {
    expect(card.get("category")).toBe("");
  });
});
