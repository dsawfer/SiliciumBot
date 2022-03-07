package com.zhivaevartem.siliciumbot.util;

import java.util.ArrayList;
import java.util.List;
import org.codehaus.plexus.util.cli.CommandLineUtils;

/**
 * Utility class to work with strings.
 */
public class StringUtils {
  /**
   * Parse command to arguments.
   *
   * @param command Space separated arguments. Content between two quotes is a single argument.
   * @return List of arguments.
   */
  public static List<String> parseArguments(String command) {
    try {
      return new ArrayList<>(List.of(CommandLineUtils.translateCommandline(command)));
    } catch (Exception e) {
      return new ArrayList<>() {{
          add("");
        }};
    }
  }

  private StringUtils() {}
}
