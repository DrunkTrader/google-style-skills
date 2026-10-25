import Foo from './foo';

export default class Bar {
  #value = new Array(1);

  get value() {
    return this.#value++;
  }
}
