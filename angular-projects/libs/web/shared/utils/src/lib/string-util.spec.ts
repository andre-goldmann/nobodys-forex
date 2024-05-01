import { StringUtil } from './string-util';

describe('getIdFromUri', () => {
  it('should return the last part of the URI after splitting by colon', () => {
    const uri = 'example:123:456';
    expect(StringUtil.getIdFromUri(uri)).toBe('456');
  });

  it('should return the last part of the URI even if it contains a colon', () => {
    const uri = 'example:123:456:789';
    expect(StringUtil.getIdFromUri(uri)).toBe('789');
  });

  it('should return the input string if no colon is found', () => {
    const uri = 'example';
    expect(StringUtil.getIdFromUri(uri)).toBe('example');
  });

  it('should return an empty string if the input string is empty', () => {
    const uri = '';
    expect(StringUtil.getIdFromUri(uri)).toBe('');
  });
});
