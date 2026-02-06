const mongoose = require("mongoose");

const productSchema = new mongoose.Schema({
  name: String,
  category: {
    type: String,
    enum: ["Plumbing", "Electrical", "Painting", "Flooring", "Sanitary"]
  },
  price: Number,
  stock: Number,
  fastDelivery: Boolean,
  image: String
});

module.exports = mongoose.model("Product", productSchema);
