#include <memory>
#include "widgets/widget.h"

using namespace widgets;

class Widget {
 public:
  Widget(Renderer* renderer) : renderer_(renderer) {}

 private:
  Renderer* renderer_;
};
