export class StackConfiguration {
  public static getHWFUsername(): string {
    return StackConfiguration.getFromEnvironment("HWF_USERNAME");
  }

  public static getHWFPassword(): string {
    return StackConfiguration.getFromEnvironment("HWF_PASSWORD");
  }
  public static getServiceName(): string {
    return "mywellness-class-booker";
  }

  private static getFromEnvironment(name: string): string {
    const value = process.env[name];

    if (value === undefined) {
      throw Error(`Environment variable ${name} is not set.`);
    }

    return value;
  }
}
