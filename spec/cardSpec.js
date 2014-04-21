describe("A default card should have a several attributes...", function() {
  var card = new app.Card();
  
  it("Should have a category.", function() {
    expect(card.get("category")).toBe("");
  });

  it("Should have a tags array.", function() {
    expect(card.get("tags") instanceof Array).toBe(true);
    expect(card.get("tags").length).toBe(0);
  });

  it("Should have content.", function() {
    expect(card.get("content")).toBe("");
  });

  it("Should have an author with a first name...", function() {
    expect(card.get("authorFirst")).toBe("first");
  });

  it("and a last name.", function() {
    expect(card.get("authorLast")).toBe("last");
  });

  it("Should have an author id assigned.", function() {
    expect(card.get("author_id")).toBe(-1);
  });

  it("Should have a post time.", function() {
    expect(card.get("post_time")).toBe("");
  });

  it("Should have a post date.", function() {
    expect(card.get("post_date")).toBe("");
  });

  it("Should have an empty 'marks' array.", function() {
    expect(card.get("marks") instanceof Array).toBe(true);
    expect(card.get("marks").length).toBe(0);
  });

  it("Should have an empty 'adds' array.", function() {
    expect(card.get("adds") instanceof Array).toBe(true);
    expect(card.get("adds").length).toBe(0);
  });

  it("Should have an empty 'comments' array.", function() {
    expect(card.get("comments") instanceof Array).toBe(true);
    expect(card.get("comments").length).toBe(0);
  });

  it("Should have a popularity value", function() {
    expect(card.get("popularity")).toBe(0);
  });
  
});
