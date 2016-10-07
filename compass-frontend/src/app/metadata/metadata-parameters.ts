import {isNullOrUndefined} from "util";

export class MetadataParameters {
  search: string;
  language: string;
  ordering: string;
  limit: number;
  page_size: number;
  page: number;
  from: number;
  to: number;
  year: string;

  clear(): void {
    this.search = this.language = this.ordering = this.limit = this.page_size = this.page = null;
  }

  private exists(value) {
    return (isNullOrUndefined(value)) || (value == '');
  }

  toUrlQuery(): string {
    var options_list: string[] = ["format=json"];

    if (!this.exists(this.search)){
      options_list.push('search=' + this.search);
    }
    if (!this.exists(this.language)){
      options_list.push('language=' + this.language);
    }
    if (!this.exists(this.ordering)){
      options_list.push('ordering=' + this.ordering);
    }
    if(!this.exists(this.limit)){
      options_list.push('limit=' + this.limit);
    }
    if(!this.exists(this.page_size)){
      options_list.push('page_size=' + this.page_size);
    }
    if(!this.exists(this.page)){
      options_list.push('page=' + this.page);
    }
    if(!this.exists(this.from)){
      options_list.push('from=' + this.from);
    }
    if(!this.exists(this.to)){
      options_list.push('to=' + this.to);
    }
    if(!this.exists(this.year)){
      options_list.push('year=' + this.year);
    }
    var query_string = options_list.join('&');
    return '?' + query_string;
  }
}
