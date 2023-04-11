


var multipleCardCarousel = document.querySelector(
  "#c-control"
);
if (window.matchMedia("(min-width: 768px)").matches) {
  var carousel = new bootstrap.Carousel(multipleCardCarousel, {
    interval: false,
  });
  var carouselWidth = $(".c-inner")[0].scrollWidth;
  var cardWidth = $(".c-item").width();
  var scrollPosition = 0;
  $("#c-control .c-next").on("click", function () {
    if (scrollPosition < carouselWidth - cardWidth * 4) {
      scrollPosition += cardWidth;
      $("#c-control .c-inner").animate(
        { scrollLeft: scrollPosition },
        600
      );
    }
  });
  $("#c-control .c-prev").on("click", function () {
    if (scrollPosition > 0) {
      scrollPosition -= cardWidth;
      $("#c-control .c-inner").animate(
        { scrollLeft: scrollPosition },
        600
      );
    }
  });
} else {
  $(multipleCardCarousel).addClass("slide");
}