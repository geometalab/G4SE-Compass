import {Pipe, PipeTransform, Sanitizer, SecurityContext} from '@angular/core';

@Pipe({
  name: 'linkify'
})
export class LinkifyPipe implements PipeTransform {
  private sanitizer: Sanitizer;

  transform(value: any, args?: any): any {
    return this.sanitizer.sanitize(SecurityContext.HTML, value);
  }

}
