import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchComponent } from './search.component';
import {SpinnerComponent} from "../../spinner/spinner.component";

@NgModule({
  imports: [
    CommonModule,
    SpinnerComponent,
  ],
  declarations: [SearchComponent],

})
export class SearchModule { }
