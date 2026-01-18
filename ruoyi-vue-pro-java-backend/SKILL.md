---
name: ruoyi-vue-pro-java-backend
description: "Guidance and standards for ruoyi-vue-pro style Java backend development with Maven. Use when adding or modifying backend code, APIs, services, or persistence logic: code must compile with Maven; every class, method, static field, and static method must have full Javadoc; object copying should prefer Hutool Convert to reduce manual getter/setter code."
---

# Ruoyi Vue Pro Java Backend

## Overview

Guide ruoyi-vue-pro backend changes to keep Maven compilation green, Javadoc complete, object copy handled by Hutool Convert, and important flows properly logged.

## Workflow

1. Read the existing module structure and naming; align with current layering (controller/service/mapper/entity).
2. If a specific module is involved, read that module's `MODULE.md` first and limit search and edits to that scope.
3. Keep changes KISS/DRY/YAGNI; avoid unnecessary complexity or duplication.
4. Add full Javadoc on every class, method, static field, and static method.
5. Prefer Hutool `Convert` for object copying to reduce manual getter/setter usage; only use alternatives when Convert cannot meet requirements, and explain why.
6. Add logs for important chains and key decision points; keep logs concise and meaningful. Use operate logs for business/admin actions.
7. Verify compilation with Maven: run `mvn -q -DskipTests compile` (or `-pl <module> -am` for a single module).

## Javadoc Requirements

- Every class, method, static field, and static method must have Javadoc.
- Keep comment language consistent with the existing codebase.
- Method Javadoc must cover intent, parameters, return value, and exceptions (if any).

Example:
```java
/**
 * User report service.
 */
public class ReportService {

    /**
     * Default page size.
     */
    private static final int DEFAULT_PAGE_SIZE = 20;

    /**
     * Fetch reports by user id.
     *
     * @param userId user id
     * @return report list
     */
    public List<Report> listByUserId(Long userId) {
        // ...
    }
}
```

## Object Copying (Hutool Convert)

- Prefer `cn.hutool.core.convert.Convert`, for example:
  - `Convert.convert(Target.class, source)`
- If Convert cannot cover complex mappings, use the simplest alternative and document the reason.

## Logging Requirements

- Important chains (e.g., core business flows, critical state transitions, external calls) must be logged.
- Use project-standard logging APIs (e.g., SLF4J) and log levels consistently.
- Keep logs concise, structured, and avoid sensitive data.
- For business/admin actions, add operate logs via `@LogRecord` in service methods (see Operate Log Requirements).

Example:
```java
@Slf4j
@Service
public class OrderService {

    /**
     * Create an order and trigger payment.
     *
     * @param createReq create request
     * @return order id
     */
    public Long createOrder(OrderCreateReq createReq) {
        log.info("Order create start, req={}", JsonUtils.toJsonString(createReq));
        Long orderId = doCreate(createReq);
        log.info("Order create success, orderId={}", orderId);
        paymentClient.pay(orderId);
        log.info("Order payment triggered, orderId={}", orderId);
        return orderId;
    }
}
```

## Operate Log Requirements

- Use `@LogRecord` from `yudao-spring-boot-starter-security` (the `operatelog` package based on `mzt-biz-log`) to record operation logs.
- Store operation logs via the system module's `OperateLog` implementation into `system_operate_log` (do not replace with plain SLF4J logs).
- Define operation log constants (e.g., sub-type and success message) in a per-module `LogRecordConstants` class to keep templates consistent and searchable.
- For update scenarios, use the `_DIFF` function in log templates and annotate request/command fields with `@DiffLogField`:
  - Set `name` to the field display name.
  - Set `function` to a parse function when translation is needed (e.g., `PostParseFunction`, `DeptParseFunction`, `SexParseFunction`).
- If unsure about patterns, reference the CRM module `LogRecordConstants` usage and the `mzt-biz-log` guide linked in the system log docs.

## Menu and Permission Data Requirements

- When adding a new page or feature that introduces menus or permissions, insert corresponding records into `system_menu`.
- Do not guess field semantics. Align with the project rules:
  - `type`: 1=目录, 2=菜单, 3=按钮.
  - `status`: 1=开启, 0=关闭.
  - `permission`: 模块:资源:动作.
- Use the same pattern as existing menus in the same module: parent structure, route `path`, `component`, and `component_name`.
- Insert both menu and permission points if the feature requires button-level permissions.
- Use SQL migration/upgrade scripts for menu data changes and keep changes idempotent.
- Prefer database defaults for `visible`, `keep_alive`, `always_show`, `create_time`, and `update_time` unless the existing module pattern explicitly overrides them.
- Keep `sort` order consistent with sibling menus and ensure `parent_id` points to a valid parent.
- Avoid hard deletes in data fixes; follow the project's delete strategy (`deleted` default/soft delete).

## Data Translation Example

Use data translation for VO fields that need display values, based on `easy-trans` annotations.

Example (module internal translation):
```java
public class OperateLogRespVO implements com.fhs.core.trans.vo.VO {

    @Trans(type = TransType.SIMPLE, target = AdminUserDO.class,
            fields = "nickname", ref = "userNickname")
    private Long userId;

    private String userNickname;
}
```

Example (cross-module translation):
```java
public class CrmProductRespVO implements com.fhs.core.trans.vo.VO {

    @Trans(type = TransType.SIMPLE,
            targetClassName = "cn.iocoder.yudao.module.system.dal.dataobject.user.AdminUserDO",
            fields = "nickname", ref = "ownerUserNickname")
    private Long ownerUserId;

    private String ownerUserNickname;
}
```

Controller return translation:
```java
@GetMapping("/page")
@TransMethodResult
public CommonResult<PageResult<OperateLogRespVO>> pageOperateLog(OperateLogPageReqVO pageReqVO) {
    PageResult<OperateLogDO> pageResult = operateLogService.getOperateLogPage(pageReqVO);
    return success(BeanUtils.toBean(pageResult, OperateLogRespVO.class));
}
```

## Build Requirement

- Changes must compile via Maven:
  - `mvn -q -DskipTests compile`
- For a single module, use `-pl <module> -am` to limit scope.
