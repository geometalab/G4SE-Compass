import {Pipe, PipeTransform} from '@angular/core';
import { LinkyPipe } from 'angular2-linky';

@Pipe({
  name: 'linkify'
})
export class LinkifyPipe extends LinkyPipe implements PipeTransform {
  // private linky: LinkyPipe;
  transform(value: any, args?: any): any {

  }

}
