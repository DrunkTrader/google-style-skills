#include "widgets/widget.h"

#include <memory>

namespace widgets {

Widget::Widget(std::unique_ptr<Renderer> renderer)
    : renderer_(std::move(renderer)) {}

}  // namespace widgets
