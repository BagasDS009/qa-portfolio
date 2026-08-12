package com.kai.config;

import java.util.Map;

/**
 * Device configurations for mobile emulation.
 * Replicates real device viewports, user agents, pixel ratio, and touch support.
 */
public class DeviceConfig {

    private final String name;
    private final int width;
    private final int height;
    private final double deviceScaleFactor;
    private final boolean isMobile;
    private final boolean hasTouch;
    private final String userAgent;

    public DeviceConfig(String name, int width, int height, double deviceScaleFactor,
                        boolean isMobile, boolean hasTouch, String userAgent) {
        this.name = name;
        this.width = width;
        this.height = height;
        this.deviceScaleFactor = deviceScaleFactor;
        this.isMobile = isMobile;
        this.hasTouch = hasTouch;
        this.userAgent = userAgent;
    }

    public String getName() { return name; }
    public int getWidth() { return width; }
    public int getHeight() { return height; }
    public double getDeviceScaleFactor() { return deviceScaleFactor; }
    public boolean isMobile() { return isMobile; }
    public boolean hasTouch() { return hasTouch; }
    public String getUserAgent() { return userAgent; }

    // --- Predefined Devices ---

    public static final DeviceConfig IPHONE_13 = new DeviceConfig(
            "iPhone 13", 390, 844, 3,
            true, true,
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    );

    public static final DeviceConfig IPHONE_14_PRO = new DeviceConfig(
            "iPhone 14 Pro", 393, 852, 3,
            true, true,
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    );

    public static final DeviceConfig PIXEL_7 = new DeviceConfig(
            "Pixel 7", 412, 915, 2.625,
            true, true,
            "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
    );

    public static final DeviceConfig GALAXY_S21 = new DeviceConfig(
            "Samsung Galaxy S21", 360, 800, 3,
            true, true,
            "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
    );

    public static final DeviceConfig IPAD_PRO = new DeviceConfig(
            "iPad Pro 11", 834, 1194, 2,
            true, true,
            "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    );

    /** Mobile devices used for parameterized tests. */
    public static final DeviceConfig[] MOBILE_DEVICES = {
            IPHONE_13, PIXEL_7, GALAXY_S21
    };

    /** Tablet devices for parameterized tests. */
    public static final DeviceConfig[] TABLET_DEVICES = {
            IPAD_PRO
    };

    /**
     * Convert to Selenium ChromeOptions mobile emulation map.
     */
    public Map<String, Object> toMobileEmulation() {
        Map<String, Object> deviceMetrics = Map.of(
                "width", width,
                "height", height,
                "pixelRatio", deviceScaleFactor,
                "mobile", isMobile,
                "touch", hasTouch
        );
        return Map.of(
                "deviceMetrics", deviceMetrics,
                "userAgent", userAgent
        );
    }

    @Override
    public String toString() {
        return name;
    }
}
