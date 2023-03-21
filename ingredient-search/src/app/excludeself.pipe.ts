import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'excludeself'
})
export class ExcludeselfPipe implements PipeTransform {

  transform(items: any[], current: any): any[] {
    if (!items) {
      return [];
    }
    return items.filter(item => item !== current);
  }

}
